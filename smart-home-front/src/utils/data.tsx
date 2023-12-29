import {
  FaFacebookF,
  FaInstagram,
  FaLinkedin,
  FaTwitter,
} from "react-icons/fa";


export const theme = {
  colors: {
    main: "#b4e854",
    secondColor: "#263d3d",
    textColor: "white",
    red: "#f54263",
    grey: "#f0f0f0",
  },
  radius: {
    buttons: "4px",
  },
  fontSizes: {
    standard: "14px",
    large: "16px",
    small: "12px",
    header: "30px",
  },
};

export const icons = [
  { href: "https://www.facebook.com", icon: <FaFacebookF /> },
  { href: "https://www.twitter.com", icon: <FaTwitter /> },
  { href: "https://www.instagram.com", icon: <FaInstagram /> },
  { href: "https://www.linkedin.com", icon: <FaLinkedin /> },
];

export const infoItems = [
  { label: "Email", value: "smartHome@gmail.com" },
  { label: "Phone", value: "+123456789" },
  { label: "Address", value: "Strumicka 6, Novi Sad" },
];
export const navbarTitle = "Smart Home";
  
  export const menuOptions = [
    { href: "", value: "Home"},
    { href: "/devices", value: "Devices"},
    { href: "/alarm", value: "Alarm Clock"},
    { href: "#", value: "Contact"},
  ];
  


