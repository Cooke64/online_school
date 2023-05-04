import React from "react";

export default function useSearch(query, itemList) {
  const searchedCourses = React.useMemo(() => {
    if (query) {
      return itemList.filter((post) =>
        post.title.toLowerCase().includes(query.toLowerCase())
      );
    }
    return itemList;
  }, [query, itemList]);
  return searchedCourses;
}
