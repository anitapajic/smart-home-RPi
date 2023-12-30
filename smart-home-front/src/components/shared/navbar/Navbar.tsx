import { useState } from "react";
import {
  NavbarStyle,
  Title,
  Menu,
  MenuItem,
  MenuLink,
  Hamburger,
} from "./Navbar.styled";
import { Link } from "react-router-dom";
import Modal from "../modal/Modal";
import SafetySystemForm from "../../safetySystemForm/SafetySystemForm";

export interface NavbarProps {
  title: string;
  label?: string;
  isMenuOpen: boolean;
  options: { href: string; value: string }[];
  footerRef?: React.RefObject<HTMLDivElement>;
  setIsMenuOpen: React.Dispatch<React.SetStateAction<boolean>>;
}

export default function Navbar({
  title,
  isMenuOpen,
  setIsMenuOpen,
  options,
  footerRef,
}: NavbarProps) {

  const [isModalVisible, setIsModalVisible] = useState(false);


  const handleContactClick = () => {
    footerRef?.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleSafetySystem = () => {
    console.log("aaa")
    setIsModalVisible(true);
  }

  const handleFormCancel = () => {
    setIsModalVisible(false);
  };

  return (
    <>
      <NavbarStyle>
        <Title as={Link} to={"/"}>
          {title}
        </Title>
        <Hamburger onClick={() => setIsMenuOpen(!isMenuOpen)}>☰</Hamburger>
        <Menu isOpen={isMenuOpen}>
          {options.map((link, index) => (
            <MenuItem key={index}>
              <MenuLink
                as={Link}
                onClick={() => {
                  if (link.value === "Contact") {
                    handleContactClick();
                  }
                  if (link.value === "Safety System") {
                    handleSafetySystem();
                  }
                  setIsMenuOpen(false);
                }}
                to={link.href}
              >
                {link.value}
              </MenuLink>
            </MenuItem>
          ))}
        </Menu>
      </NavbarStyle>
      <Modal isVisible={isModalVisible} onClose={handleFormCancel}>
        <SafetySystemForm onSubmit={handleFormCancel}></SafetySystemForm>
      </Modal>
    </>
  );
}
