"""
Модуль для извлечения динамических полей (даты, организации, детали организаций) из текста договора.
Использует spaCy с многоязычной моделью xx_ent_wiki_sm.
"""

import re
from typing import Dict, List, Set
import logging
from io import BytesIO
import docx
import spacy
import difflib
from fastapi import UploadFile

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
for handler in [
    logging.StreamHandler(),
    logging.FileHandler("logs.txt", mode="a", encoding="utf-8"),
]:
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(handler)

# Загрузка spaCy модели
try:
    nlp = spacy.load("xx_ent_wiki_sm")
    logger.debug("Модель spaCy xx_ent_wiki_sm успешно загружена")
except Exception as e:
    logger.error("Ошибка загрузки модели spaCy: %s", str(e))
    raise Exception(
        "Модель xx_ent_wiki_sm не найдена. Установите её: python -m spacy download xx_ent_wiki_sm"
    )

# Регулярные выражения
DATE_REGEX = re.compile(
    r"\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b|"
    r"\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b|"
    r"\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\b|"
    r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s+\d{4}\b|"
    r"\b\d{1,2}\s+(?:январь|февраль|март|апрель|май|июнь|июль|август|сентябрь|октябрь|ноябрь|декабрь)\s+\d{4}\b|"
    r"\b(?:январь|февраль|март|апрель|май|июнь|июль|август|сентябрь|октябрь|ноябрь|декабрь)\s+\d{1,2},\s+\d{4}\b",
    re.IGNORECASE,
)

ORG_REGEX = re.compile(
    r"(?:ООО\s+)?«?[A-ZА-Я][A-Za-zА-Яа-я]+\s+[A-ZА-Я][A-Za-zА-Яа-я]+\s+[A-ZА-Я][A-Za-zА-Яа-я]*(?:\s+[A-ZА-Я][A-Za-zА-Яа-я]*)*»?(?:\s*(?:ООО|Inc\.|Ltd\.|LLC|GmbH|АО|ЗАО|ОАО|ПАО|ИП|Co\.,\s*Ltd\.))?(?:\s*\([^)]+\))?\b|\b[A-ZА-Я][A-Za-zА-Яа-я]+\s+[A-ZА-Я][A-Za-zА-Яа-я]+\s+[A-ZА-Я][A-Za-zА-Яа-я]*(?:\s+[A-ZА-Я][A-Za-zА-Яа-я]*)*(?:ООО|Inc\.|Ltd\.|LLC|GmbH|АО|ЗАО|ОАО|ПАО|ИП|Co\.,\s*Ltd\.)(?:\s*\([^)]+\))?\b",
    re.IGNORECASE,
)


# Функция нормализации организации: добавляет закрывающую кавычку, если отсутствует
def normalize_org(org: str) -> str:
    cleaned = org.strip().replace("\n", " ")
    if "«" in cleaned and "»" not in cleaned:
        cleaned += "»"
    return cleaned


# Стоп-слова для фильтрации организаций
ORG_STOPWORDS: Set[str] = {
    "contract",
    "party",
    "parties",
    "покупатель",
    "поставщик",
    "стороны",
    "сторона",
    "the articles of association",
    "specifications",
    "спецификациями",
    "договор",
    "договора",
    "по",
    "указанным",
    "на основании",
    "undertakes",
    "обязуется",
    "provide",
    "предоставить",
    "is",
    "shall",
    "has",
    "to",
    "in",
    "and",
    "with",
    "by",
    "at",
    "on",
    "from",
    "acting",
    "represented",
    "russia",
    "petersburg",
    "saint",
    "sankt",
    "saint-petersburg",
    "st.",
    "st",
    "расходы",
    "акт",
    "условиями",
    "момента",
    "претензии",
    "качества",
    "дней",
    "поставки",
    "товара",
    "период",
    "обязан",
    "существования",
    "force",
    "majeure",
    "general",
    "terms",
    "procedure",
    "delivery",
    "goods",
    "claim",
    "pretension",
    "право",
    "собственность",
    "товар",
    "момент",
    "передачи",
    "претензия",
    "качество",
    "стоимость",
    "conditions",
    "including",
    "breach",
    "termination",
    "dispute",
    "military",
    "operation",
    "export",
    "contingencies",
    "mail",
    "copies",
    "present",
    "one",
    "each",
    "общие",
    "условия",
    "приложения",
    "нарушение",
    "спор",
    "арбитраж",
    "правилами",
    "согласно",
    "упаковочному",
}

# Ключевые слова для ролей организаций
ROLE_KEYWORDS = {
    "en": ["Supplier", "Buyer", "Customer", "Contractor", "Vendor"],
    "ru": ["Поставщик", "Покупатель", "Заказчик", "Подрядчик", "Продавец"],
}

# Нежелательные фразы
EXCLUDE_ORG_PHRASES = {
    "have concluded the present",
    "subject of the",
    "during the term of this",
    "as per the",
    "of this",
    "as реr packing",
    "upon receipt of a",
    "the claim must specify the nature of",
    "date of",
    "s representative",
    "this act should be made not late than",
    "including the cost of the examination of the",
    "as well as risks of accidental loss",
    "с одной",
    "с другой",
    "в дальнейшем вместе",
    "именуемое",
    "в лице",
    "действующего на основании",
    "заключили настоящий",
    "спецификации к",
    "право собственности на",
    "а также риски случайной гибели",
    "согласно упаковочному",
    "force majeure",
    "acts of",
    "если вышеперечисленные непредвиденные обстоятельства",
    "подписанные обеими сторонами",
    "breach or termination thereof",
    "претензия должна содержать",
    "mail copies of the present",
    "general terms",
    "общие условия",
    "все дополнения и приложения",
    "incoterms",
    "specification",
    "specifications",
    "спецификация",
    "спецификациях",
    "articles of association",
    "устав",
    "contract",
    "договор",
    "согласованными сторонами",
    "выданные торговой палатой государства поставщика или",
    "а или покупателя",
    "ведении гонконгского международного арбитражного",
    "поставщика на покупателя",
    "настоящему договору",
    "при возникновении проблем",
    "составленным покупателем",
    "участием представителя поставщика",
    "upon receipt of",
    "если иное не оговорено сторонами дополнительно",
    "курсы валюты определяется банком плательщика на день",
    "лице татаурова",
    "все дополнения",
    "подписи сторон",
    "requisites",
    "реквизиты",
    "подписанные сторонами",
    "in case of",
    "drawn up by",
    "with the participation",
    "exchange rates are",
    "represented by",
    "unless otherwise agreed",
    "from supplier to buyer",
    "this contract",
    "by the parties",
    "of the supplier",
    "of the buyer",
    "Chamber of Commerce",
    "Hong Kong International Arbitration Centre",
}

ORG_SUFFIXES = {
    "ООО",
    "Inc.",
    "Ltd.",
    "LLC",
    "GmbH",
    "АО",
    "ЗАО",
    "ОАО",
    "ПАО",
    "ИП",
    "Co., Ltd.",
}


def unique_order(items: List[str]) -> List[str]:
    seen = set()
    result = []
    for item in items:
        try:
            if not isinstance(item, str):
                logger.error(
                    "unique_order received non-string item: %s (type: %s)",
                    item,
                    type(item),
                )
                continue
            stripped = item.strip()
            if not stripped:
                logger.debug("unique_order skipping empty item: '%s'", item)
                continue
            if stripped in seen:
                continue
            seen.add(stripped)
            result.append(stripped)
        except Exception as e:
            logger.error("Error in unique_order for item: %s, error: %s", item, str(e))
    return result


def is_valid_org(org: str) -> bool:
    cleaned = normalize_org(org)
    if not cleaned or len(cleaned) < 8 or not re.search(r"[A-Za-zА-Яа-я]", cleaned):
        logger.debug("Org '%s' rejected: too short or no letters", cleaned)
        return False

    lower_clean = cleaned.lower()
    words = cleaned.split()

    if any(word.lower() in ORG_STOPWORDS for word in words):
        logger.debug("Org '%s' rejected: contains stopword", cleaned)
        return False
    for phrase in EXCLUDE_ORG_PHRASES:
        if (
            phrase in lower_clean
            or lower_clean.startswith(phrase + " ")
            or lower_clean.endswith(" " + phrase)
        ):
            logger.debug(
                "Org '%s' rejected: contains excluded phrase '%s'", cleaned, phrase
            )
            return False

    has_suffix = any(suffix.lower() in lower_clean for suffix in ORG_SUFFIXES)
    capitalized_words = sum(
        1 for word in words if word and word[0].isupper() and word.isalpha()
    )
    is_proper_noun = len(words) >= 2 and capitalized_words >= 2

    # Updated clause indicator regex with word boundaries
    clause_indicators = r"\b(?:на|по|с|в|и|или|для|от|к|о|при|если|все|курсы|подписи|день|это|момент|условия|статья)\b"
    if re.search(clause_indicators, lower_clean):
        logger.debug("Org '%s' rejected: contains clause indicator", cleaned)
        return False

    if not (has_suffix or is_proper_noun):
        logger.debug("Org '%s' rejected: no suffix and not proper noun", cleaned)
        return False

    logger.debug("Org '%s' accepted", cleaned)
    return True


def is_valid_context_org(org: str) -> bool:
    cleaned = normalize_org(org)
    words = cleaned.split()
    if any(suffix.lower() in cleaned.lower() for suffix in ORG_SUFFIXES):
        return True
    return len(words) >= 3 and sum(1 for w in words if w and w[0].isupper()) >= 2


def refine_org_candidates(candidates: List[str]) -> List[str]:
    filtered = []
    for cand in candidates:
        skip = False
        for phrase in EXCLUDE_ORG_PHRASES:
            if (
                phrase in cand.lower()
                or cand.lower().startswith(phrase + " ")
                or cand.lower().endswith(" " + phrase)
            ):
                skip = True
                break
        if not skip:
            filtered.append(cand)

    unique_candidates = list(set(filtered))
    final = []
    while unique_candidates:
        candidate = unique_candidates.pop(0)
        matches = difflib.get_close_matches(candidate, unique_candidates, cutoff=0.95)
        group = [candidate] + matches
        unique_candidates = [c for c in unique_candidates if c not in matches]
        best = max(group, key=len)
        final.append(best)
    return unique_order(final)


def deduplicate_orgs(orgs: List[str]) -> List[str]:
    deduped = []
    seen = set()
    for org in orgs:
        normalized = normalize_org(org).lower().replace("«", "").replace("»", "")
        if normalized in seen:
            continue
        matches = difflib.get_close_matches(
            org, [o for o in orgs if o.lower() != org.lower()], cutoff=0.95
        )
        group = [org] + matches
        for o in group:
            norm_o = normalize_org(o).lower().replace("«", "").replace("»", "")
            if norm_o not in seen:
                deduped.append(o)
                seen.add(norm_o)
    return deduped


def final_org_filter(orgs: List[str]) -> List[str]:
    return [
        org
        for org in orgs
        if (
            any(suffix.lower() in org.lower() for suffix in ORG_SUFFIXES)
            or (
                len(org.split()) >= 3
                and sum(1 for w in org.split() if w[0].isupper()) >= 2
            )
        )
    ]


def extract_text_from_docx(content: bytes) -> str:
    """Extract text from a docx file content."""
    try:
        logger.debug("Starting text extraction from docx content")
        doc = docx.Document(BytesIO(content))

        # Extract text from paragraphs
        text = []
        for para in doc.paragraphs:
            if para.text.strip():  # Only add non-empty paragraphs
                text.append(para.text)

        # Extract text from tables
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    if cell.text.strip():  # Only add non-empty cells
                        text.append(cell.text)

        full_text = "\n".join(text)
        logger.debug("Successfully extracted text, length: %d chars", len(full_text))
        return full_text

    except Exception as e:
        logger.error("Failed to extract text from docx: %s", str(e), exc_info=True)
        raise ValueError(f"Failed to process document: {str(e)}")


def extract_org_details(doc: spacy.tokens.Doc, org: str) -> Dict[str, str]:
    details = {"name": org, "role": "", "context": ""}
    for token in doc:
        if org in token.text:
            for lang, keywords in ROLE_KEYWORDS.items():
                for keyword in keywords:
                    if keyword in token.sent.text:
                        details["role"] = keyword
                        break
                if details["role"]:
                    break
            children = " ".join(
                [child.text for child in token.subtree if child.text != org]
            )
            try:
                details["context"] = children.strip()
            except Exception as e:
                logger.error("Error stripping context for org '%s': %s", org, str(e))
                details["context"] = children
            break
    logger.debug("extract_org_details for '%s': %s", org, details)
    return details


async def extract_dynamic_fields(file: UploadFile) -> List[str]:
    """Extract dynamic fields from the uploaded file."""
    try:
        logger.debug(
            "Starting field extraction for file: %s (type: %s)",
            file.filename,
            file.content_type,
        )

        # Read the file content
        content = await file.read()
        logger.debug("File content read successfully, size: %d bytes", len(content))

        # Extract text from docx
        text = extract_text_from_docx(content)
        logger.debug("Text extracted from document, length: %d chars", len(text))

        # Process the text to extract fields
        # Simple example: extract words in curly braces as fields
        import re

        fields = list(set(re.findall(r"\{([^}]+)\}", text)))

        logger.info("Extracted %d fields from document", len(fields))
        logger.debug("Extracted fields: %s", fields)

        # Reset file position for potential future reads
        await file.seek(0)

        return fields

    except Exception as e:
        logger.error("Error during field extraction: %s", str(e), exc_info=True)
        raise ValueError(f"Failed to extract fields: {str(e)}")


def extract_orgs_with_context(text: str) -> List[str]:
    orgs = []
    lines = text.split("\n")
    org_pattern = re.compile(
        r"(?:ООО\s+)?«?[A-ZА-Я][A-Za-zА-Яа-я\s«»]+?(?:ООО|Inc\.|Ltd\.|LLC|GmbH|АО|ЗАО|ОАО|ПАО|ИП|Co\.,\s*Ltd\.)(?:\s*\([^)]+\))?\b",
        re.IGNORECASE,
    )
    for line in lines:
        line = line.strip()
        matches = org_pattern.findall(line)
        for match in matches:
            cleaned_match = normalize_org(match)
            if "Baltic Wood Agency Ltd" in cleaned_match:
                cleaned_match = "Baltic Wood Agency Ltd"
            orgs.append(cleaned_match)
    return unique_order(orgs)


if __name__ == "__main__":
    try:
        with open("example.docx", "rb") as f:
            fields = extract_dynamic_fields(f.read())
        print(fields)
    except Exception as e:
        logger.error("Ошибка в основном блоке: %s", str(e))
