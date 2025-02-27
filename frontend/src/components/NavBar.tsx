import React from 'react';
import { Link } from 'react-router-dom';
import { Layout, Menu } from 'antd';
import logo from '../assets/logo-min.png'; // Import the logo image

const { Header } = Layout;

/**
 * Navbar component renders a fixed navigation bar with a logo and navigation links.
 */
const Navbar: React.FC = () => {
  const menuItems = [
    { key: '1', label: <Link to="/">Home</Link> },
    { key: '2', label: <Link to="/about">About</Link> },
    { key: '3', label: <Link to="/contact">Contact</Link> },
    { key: '4', label: <Link to="/services">Services</Link> },
  ];

  return (
    <Header className="navbar" style={{ backgroundColor: 'white' }}>
      <div className="navbar-container">
        <div className="navbar-logo">
          <Link to="/">
            <img src={logo} alt="Logo" />
          </Link>
        </div>
        <Menu className="navbar-menu" mode="horizontal" items={menuItems} />
      </div>
    </Header>
  );
};

export default Navbar;
