import React from "react";
import cls from "./Loader.module.css";
import CircularProgress from "@mui/material/CircularProgress";

export default function Loader() {
  return (
    <div className={cls.loader_div}>
      <CircularProgress className={cls.loader} size='10rem'/>
      
    </div>
  );
}
