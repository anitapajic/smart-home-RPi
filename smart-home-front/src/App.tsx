import { useState, useRef } from 'react';
import './App.css';
import Navbar from './components/shared/navbar/Navbar';
import { theme, navbarTitle, menuOptions, icons, infoItems } from './utils/data';
import MyRoutes from "./utils/routes";
import { BrowserRouter as Router } from "react-router-dom";
import { AppContainer, ContentContainer } from './App.styled';
import { ThemeProvider } from 'styled-components';
import { MantineProvider } from "@mantine/core";
import Footer from './components/shared/footer/Footer';

function App() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const footerRef = useRef(null);

  return (
    <>
      <ThemeProvider theme={theme}>
        <MantineProvider>
          <Router>
            <AppContainer className="App">
              <Navbar
                footerRef={footerRef}
                title={navbarTitle}
                options={menuOptions}
                isMenuOpen={isMenuOpen}
                setIsMenuOpen={setIsMenuOpen}
              />
              <ContentContainer isMenuOpen={isMenuOpen}>
                <MyRoutes />
              </ContentContainer>
              <Footer ref={footerRef} icons={icons} infoItems={infoItems} />
            </AppContainer>
          </Router>
        </MantineProvider>
      </ThemeProvider>
    </>
  );
}

export default App;
