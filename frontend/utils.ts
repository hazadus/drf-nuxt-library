export function useFormatDateTime(dateObj: Date) {
  // Return `dateObj` formatted to string like "01.05.2023 18:31".
  let date = new Date(dateObj);
  return (
    date.toLocaleDateString("ru-RU") +
    " " +
    date.toLocaleTimeString("ru-RU", {
      hour: "2-digit",
      minute: "2-digit",
    })
  );
}
