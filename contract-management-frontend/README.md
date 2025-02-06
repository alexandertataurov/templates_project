# 🚀 Проект: [Название проекта]

## 📌 Описание
Этот проект предназначен для управления шаблонами документов, включая их создание, редактирование, загрузку и удаление.

## 🏗 Структура проекта
```
📂 src
 ┣ 📂 api          # API-запросы и хуки
 ┃ ┣ 📜 config.ts      # Базовая конфигурация API
 ┃ ┗ 📜 templates.ts   # API-хуки для работы с шаблонами
 ┣ 📂 components    # UI-компоненты
 ┃ ┣ 📜 EditTemplate.tsx   # Компонент редактирования шаблона
 ┃ ┣ 📜 FileUploader.tsx   # Загрузчик файлов
 ┃ ┣ 📜 Loader.tsx         # Индикатор загрузки
 ┃ ┣ 📜 Navbar.tsx        # Навигационное меню
 ┃ ┗ 📜 ToastProvider.tsx # Уведомления
 ┣ 📂 pages         # Страницы приложения
 ┃ ┣ 📜 Home.tsx           # Главная страница
 ┃ ┣ 📜 CheckStatus.tsx    # Проверка статуса шаблонов
 ┃ ┣ 📜 ManageFields.tsx   # Управление полями
 ┃ ┣ 📜 UploadTemplate.tsx # Загрузка шаблонов
 ┃ ┗ 📜 WizardPage.tsx     # Мастер создания
 ┣ 📂 wizard       # Пошаговый мастер (Wizard)
 ┃ ┣ 📜 Wizard.tsx      # Контроллер мастера
 ┃ ┣ 📜 WizardStep1.tsx # Добавление полей
 ┃ ┣ 📜 WizardStep2.tsx # Инструкция
 ┃ ┗ 📜 WizardStep3.tsx # Загрузка шаблона
 ┣ 📂 styles       # Глобальные стили
 ┃ ┣ 📜 App.css      # Основные стили
 ┃ ┗ 📜 index.css    # Базовые стили
 ┣ 📜 router.tsx    # Конфигурация маршрутизации
 ┣ 📜 App.tsx       # Главный компонент приложения
 ┣ 📜 main.tsx      # Точка входа в приложение
📂 public          # Статические файлы
📂 config          # Конфигурационные файлы
 ┣ 📜 .eslintrc.json  # Конфигурация ESLint
 ┣ 📜 .prettierrc     # Конфигурация Prettier
 ┣ 📜 tailwind.config.js # Конфигурация TailwindCSS
 ┣ 📜 tsconfig.json   # Основной TypeScript конфиг
 ┣ 📜 vite.config.ts  # Конфигурация Vite
 ┗ 📜 .gitignore      # Исключённые файлы
```

## 🔗 Связи и зависимости между модулями
### 📂 API
- `config.ts` экспортирует `API_BASE_URL`, который используется во всех API-запросах.
- `templates.ts` содержит `fetchAPI`, который вызывает API через `useQuery` и `useMutation`.

### 📂 Components
- `EditTemplate.tsx` использует `useUpdateTemplate` из API для обновления данных шаблона.
- `FileUploader.tsx` передает файлы в `uploadTemplate` API.
- `Navbar.tsx` содержит навигацию с помощью `react-router-dom`.
- `ToastProvider.tsx` управляет глобальными уведомлениями через `react-toastify`.

### 📂 Pages
- `Home.tsx` использует `useTemplates` API для загрузки списка шаблонов.
- `CheckStatus.tsx` обращается к `useCheckStatus` API.
- `ManageFields.tsx` вызывает `defineFields` API для управления динамическими полями.
- `UploadTemplate.tsx` отправляет данные через `uploadTemplate` API.
- `WizardPage.tsx` использует `Wizard.tsx` для создания нового шаблона.

### 📂 Wizard
- `Wizard.tsx` управляет переходами между `WizardStep1.tsx`, `WizardStep2.tsx`, `WizardStep3.tsx`.
- `WizardStep1.tsx` сохраняет данные в `localStorage` и отправляет их в `defineFields` API.
- `WizardStep3.tsx` загружает файл через `uploadTemplate` API.

### 📂 Главные файлы приложения
- `router.tsx` настраивает маршруты с `React Router`.
- `App.tsx` управляет глобальным состоянием и UI.
- `main.tsx` инициализирует приложение и подключает глобальные провайдеры (`react-query`, `BrowserRouter`).

## 🚀 Установка и запуск
### 1. Установите зависимости:
```sh
npm install
```
### 2. Запустите проект в режиме разработки:
```sh
npm run dev
```
### 3. Сборка проекта:
```sh
npm run build
```

## 📡 API
Этот проект использует REST API для работы с шаблонами. Базовый URL:
```
http://localhost:8000/templates
```

## 🎨 Используемые технологии
- ⚛️ **React** – фронтенд-фреймворк
- 🌿 **TypeScript** – строгая типизация
- 🎨 **TailwindCSS** – стилизация
- 🔄 **React Query** – управление API-запросами
- 🏗 **Vite** – инструмент сборки
- 🛠 **ESLint & Prettier** – линтинг и форматирование кода