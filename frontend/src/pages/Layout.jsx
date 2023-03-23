import React from "react";
import { Outlet } from "react-router-dom";


import Footer from "components/footer/Footer";
import Header from "components/header/Header";

export default function Layout() {
  return (
    <>
      <header>
        <Header />
      </header>
      <main className="wrapper">
        <Outlet />
      </main>
      <footer>
        <Footer />
      </footer>
    </>
  );
}