import { useContext } from "react";
import AuthContext from "../services/context";

const useAuth = () => {
    return useContext(AuthContext);
}

export default useAuth;