import React from "react";
import { Outlet } from "react-router-dom";


import Footer from "components/footer/Footer";
import Navbar from "components/header/Header";

export default function Layout() {
  return (
    <>
      <header>
        <Navbar />
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