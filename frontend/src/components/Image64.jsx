import React from "react";

export default function Image64({ className, data}) {
  return (
    <img
      src={`data:image/png;base64,${data}`}
      alt="image_course"
      className={className}
    />
  );
}
