import {
  FaFacebookF,
  FaInstagram,
  FaLinkedin,
  FaTwitter,
} from "react-icons/fa";


export const theme = {
  colors: {
    main: "#6096e6",
    secondColor: "#22252b",
    textColor: "#cac9d9",
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
  { href: "", value: "Home" },
  { href: "#", value: "Safety System" },
  { href: "/devices", value: "Devices" },
  { href: "#", value: "Alarm Clock" },
  { href: "#", value: "Contact" },
];


export const urls = [
  { type: "DHT", url: "http://localhost:3000/d/a144c6c1-3619-4fc7-9881-3a2e06fb2891/dht?orgId=1&from=1703866574605&to=1703888174605" },
  { type: "PIR", url: "http://localhost:3000/d/ec447d9e-a63b-466e-a8d7-532312972770/pir?orgId=1&from=1703877507185&to=1703888307185" },
  { type: "DUS", url: "http://localhost:3000/d/c421b301-67d0-474c-9fa4-18c7b0dee2e1/dus?orgId=1&from=1703868109124&to=1703889709124" },
  { type: "DS", url: "http://localhost:3000/d/ad995c1e-b01b-459d-8986-08e4dd22cca8/door-sensor?orgId=1&from=1703885970494&to=1703889570495" },
  { type: "DL", url: "http://localhost:3000/d/adccfa99-5764-4169-b731-0452ffd92f2d/dl?orgId=1&from=1706026713675&to=1706048313675&viewPanel=1" },
  { type: "LCD", url: "http://localhost:3000/d/dfdc0928-3711-4d17-a523-e41461bbb30a/lcd?orgId=1&from=1706027300473&to=1706048900473&viewPanel=1" },
  { type: "GYRO", url: "http://localhost:3000/d/f32e53ea-d2d9-4ffe-8d05-6af522383f13/gyro?orgId=1&from=1706027486639&to=1706049086639&viewPanel=1" },
  { type: "RGB", url: "http://localhost:3000/d/d47c1e8a-ec21-4eb5-a0e9-01a901383f5a/rgb?orgId=1&from=1703886145925&to=1703889745925&viewPanel=1" },
  { type: "IR", url: "http://localhost:3000/d/b9815f28-d25e-465a-8e6b-e0417faf2a8f/ir?orgId=1&from=1706027598104&to=1706049198104&viewPanel=1" },
  { type: "4SG", url: "http://localhost:3000/d/eb76ac67-f700-4914-8eca-e0bc916c16fb/b4sd?orgId=1&from=1706028085385&to=1706049685385&viewPanel=1" },
  { type: "MS", url: "" },


]
export const devices = [
  { id: "RDHT1", name: "Room DHT 1", piNumber: 1, type: "DHT" },
  { id: "RDHT2", name: "Room DHT 2", piNumber: 1, type: "DHT" },
  { id: "RDHT3", name: "Room DHT 3", piNumber: 2, type: "DHT" },
  { id: "RDHT4", name: "Room DHT 4", piNumber: 3, type: "DHT" },
  { id: "GDHT", name: "Garage DHT", piNumber: 2, type: "DHT" },

  { id: "DPIR1", name: "Door PIR 1", piNumber: 1, type: "PIR" },
  { id: "DPIR2", name: "Door PIR 2", piNumber: 2, type: "PIR" },
  { id: "RPIR1", name: "Room PIR 1", piNumber: 1, type: "PIR" },
  { id: "RPIR2", name: "Room PIR 2", piNumber: 2, type: "PIR" },
  { id: "RPIR3", name: "Room PIR 3", piNumber: 2, type: "PIR" },
  { id: "RPIR4", name: "Room PIR 4", piNumber: 3, type: "PIR" },

  { id: "DUS1", name: "Door Ultrasonic Sensor 1", piNumber: 3, type: "DUS", url: "" },
  { id: "DUS2", name: "Door Ultrasonic Sensor 2", piNumber: 3, type: "DUS", url: "" },

  { id: "DS1", name: "Door Sensor 1", piNumber: 3, type: "DS", url: "" },
  { id: "DS2", name: "Door Sensor 2", piNumber: 3, type: "DS", url: "" },

  { id: "DL", name: "Door Light", piNumber: 1, type: "DL", url: "" },

  { id: "GLCD", name: "Garage LCD", piNumber: 2, type: "LCD", url: "" },

  { id: "GRG", name: "Gun Safe Gyro", piNumber: 2, type: "GYRO", url: "" },

  { id: "BRGB", name: "Bedroom RGB", piNumber: 3, type: "RGB", url: "" },

  { id: "BIR", name: "Bedroom Infrared", piNumber: 3, type: "IR", url: "" },

  { id: "B4SG", name: "Bedroom 4 Digit 7 Segment Display", piNumber: 3, type: "4SG", url: "" },

  { id: "DMS", name: "Door Membrane Switch", piNumber: 1, type: "MS", url: "" },











]



