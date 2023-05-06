import AuthContext from "../services/context"
import { useContext } from "react"
import { useLocation, Navigate, Outlet } from "react-router-dom"


const RequiredAuth = () => {
  const {isAuth} = useContext(AuthContext)
  const location = useLocation();

  return (
    isAuth.isUser
        ? <Outlet />
        : <Navigate to="/login" state={{ from: location }} replace />
);
}
export default RequiredAuth
