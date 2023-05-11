import React from "react";
import useAuth from "../../hooks/useAuth";
import StudentProfile from "./StudentProfile/StudentProfile";
import TeacherProfile from "./TeacherProfile/TeacherProfile";

export default function ProfilePage() {
  const { isAuth } = useAuth();

  return (
    <>
      {isAuth.userData.role === "Student" ? (
        <StudentProfile />
      ) : (
        <TeacherProfile />
      )}
    </>
  );
}
