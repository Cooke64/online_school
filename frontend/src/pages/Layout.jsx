import React from "react";
import { Outlet } from "react-router-dom";


import Footer from "components/footer/Footer";
import Header from "components/header/Header";

export default function Layout() {
  const [searchData, setSearchData] = React.useState('');
  
  const addSearchData = (data) => {
    setSearchData(data)
  }
  return (
    <>
      <header>
        <Header addSearchData={addSearchData}/>
      </header>
      <main className="wrapper">
        <Outlet context={[searchData, setSearchData]}/>
      </main>
      <footer>
        <Footer />
      </footer>
    </>
  );
}