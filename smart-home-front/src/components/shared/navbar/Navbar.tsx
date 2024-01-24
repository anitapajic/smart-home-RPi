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
import AlarmClockForm from "../../alarmClockForm/AlarmClockForm";

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
  const [isModalVisibleClock, setIsModalVisibleClock] = useState(false);

  const [isAlarm, setIsAlarm] = useState(true);
  const [isClockOn, setIsClockOn] = useState(true);

  const [socket, setSocket] = useState<Socket | null>(null);


  useEffect(() => {
    const socket = io("http://localhost:8085");


    socket.on("connect", () => {
      console.log("Connected to WebSocket");

      // Subscribe to the "/alarm" topic
      socket.emit("subscribe", "alarm");
      socket.emit("subscribe", "clock");
    });

    socket.on("disconnect", () => {
      console.log("Disconnected from WebSocket");
    });

    socket.on("alarm_message", (message) => {
      if (!isModalVisible) {
        setIsAlarm(true)
        setIsModalVisible(true);
      }

    });

    socket.on("clock_message", (message) => {
      if (!isModalVisibleClock) {
        setIsClockOn(true)
        setIsModalVisibleClock(true);
      }

    });

    socket.on("alarm_off_message", (message) => {
      setIsAlarm(false)
      setIsModalVisible(false);
    });

    socket.on("clock_off_message", (message) => {
      setIsClockOn(false)
      setIsModalVisibleClock(false);
    });

    setSocket(socket);

    return () => {
      // Disconnect the socket when the component unmounts
      socket.disconnect();
    };
  }, []);


  const handlePinEnter = (pin: string) => {
    if (isAlarm) {
      Service.deactivateAlarm(pin).then(response => {
      }).catch(error => {
        console.error("Error: ", error)
      })
    } else {
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

  const handleAlarmClock = () => {
    setIsModalVisibleClock(true);
    setIsClockOn(false)
  }
  const handleClockCancel = () => {
    setIsModalVisibleClock(false);
    setIsClockOn(true);
  };

  const handleAlarmClockEnter = (time?: string) => {
    if (isClockOn) {
      Service.turnOffAlarmClock().then(response => {
        console.log(response.data);
        setIsModalVisibleClock(false);
      }).catch(error => {
        console.error("Error: ", error)
      })
    }
    else {
      if (time) {
        Service.setAlarmClock(time).then(response => {
          console.log(response.data);
          setIsModalVisibleClock(false);
        }).catch(error => {
          console.error("Error: ", error)
        })
      }
    }

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
                  if (link.value === "Alarm Clock") {
                    handleAlarmClock();
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
      <Modal isVisible={isModalVisibleClock} onClose={handleClockCancel}>
        <AlarmClockForm onSubmit={handleAlarmClockEnter} isClockOn={isClockOn}></AlarmClockForm>
      </Modal>
      <Modal isVisible={isModalVisible} onClose={handleFormCancel}>
        <SafetySystemForm onSubmit={handlePinEnter} isAlarm={isAlarm}></SafetySystemForm>
      </Modal>

    </>
  );
}
