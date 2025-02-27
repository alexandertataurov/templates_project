import React from 'react';
import { Link } from 'react-router-dom';
import { Layout, Menu } from 'antd';

const { Header } = Layout;

/**
 * Navbar component renders a fixed navigation bar with links.
 * It uses the Menu `items` prop (instead of children) as recommended by Ant Design.
 */
const Navbar: React.FC = () => {
  const menuItems = [
    {
      key: '1',
      label: <Link to="/">Home</Link>,
    },
    {
      key: '2',
      label: <Link to="/about">About</Link>,
    },
    {
      key: '3',
      label: <Link to="/contact">Contact</Link>,
    },
  ];

  return (
    <Header style={{ position: 'fixed', zIndex: 1, width: '100%' }}>
      {/* Logo area */}
      <div
        className="logo"
        style={{
          float: 'left',
          width: '120px',
          height: '31px',
          margin: '16px 24px 16px 0',
          background: 'rgba(255, 255, 255, 0.2)',
        }}
      />
      <Menu theme="dark" mode="horizontal" items={menuItems} />
    </Header>
  );
};

export default Navbar;
