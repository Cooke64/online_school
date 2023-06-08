import './App.css';
import AppRoutes from "./pages/AppRoutes";
import React from 'react';
import AuthContext from './services/context';
import api from './api/api';
function App() {
  const [isAuth, setisAuth] = React.useState({
    isUser: false,
    userData: {
      emai: "",
      first_name: '',
      last_name: '',
      is_active: true,
      role: '',
      username: ''
    }
  })

  React.useEffect(() => {
    if (localStorage.getItem('token')){
      api.getMe().then((res) => {
        setisAuth({ isUser: true, userData: res });
      })
      .catch(err => console.log(err));
  }}, [isAuth.isUser])


  return (
    <AuthContext.Provider value={{isAuth, setisAuth}}>
        <AppRoutes/>
    </AuthContext.Provider>
  );
}

export default App;