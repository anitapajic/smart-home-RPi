import { useEffect, useRef, useState } from "react";
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
import { Socket, io } from "socket.io-client";
import Service from "../../../services/Service";

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
  const [isAlarm, setIsAlarm] = useState(true);
  const [socket, setSocket] = useState<Socket | null>(null);


  useEffect(() => {
    const socket = io("http://localhost:8085");


    socket.on("connect", () => {
      console.log("Connected to WebSocket");

      // Subscribe to the "/alarm" topic
      socket.emit("subscribe", "alarm");
    });

    socket.on("disconnect", () => {
      console.log("Disconnected from WebSocket");
    });

    socket.on("alarm_message", (message) => {
      if(!isModalVisible){
        setIsAlarm(true)
        setIsModalVisible(true);
      }
     
    });

    socket.on("alarm_off_message", (message) => {
      setIsAlarm(false)
      setIsModalVisible(false);
    });

    setSocket(socket);

    return () => {
      // Disconnect the socket when the component unmounts
      socket.disconnect();
    };
  }, []);


  const handlePinEnter = (pin : string) => {
    if(isAlarm){
      Service.deactivateAlarm(pin).then(response => {
      }).catch(error => {
          console.error("Error: ", error)
      })
  }else{
      Service.setSafetySystem(pin).then(response => {
          console.log(response.data)
          setIsModalVisible(false)

      }).catch(error => {
          console.error("Error: ", error)
      })
  }
}

  const handleContactClick = () => {
    footerRef?.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleSafetySystem = () => {
    setIsModalVisible(true);
    setIsAlarm(false)
  }

  const handleFormCancel = () => {
    setIsModalVisible(false);
    setIsAlarm(true)
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
        <SafetySystemForm onSubmit={handlePinEnter} isAlarm={isAlarm}></SafetySystemForm>
      </Modal>
    </>
  );
}
