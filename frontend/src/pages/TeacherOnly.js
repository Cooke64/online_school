import AuthContext from "../services/context"
import { useContext } from "react"
import { useLocation, Navigate, Outlet } from "react-router-dom"


const TeacherOnly = () => {
  const {isAuth} = useContext(AuthContext)
  const location = useLocation();

  return (
    isAuth.userData.role === 'Teacher'
        ? <Outlet />
        : <Navigate to="/courses" state={{ from: location }} replace />
);
}
export default TeacherOnly
