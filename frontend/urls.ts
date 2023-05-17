import { ID } from "@/types";

export function useBookDetailPageUrl(bookId: ID | string) {
  // Return URL for Book detail page.
  return `/books/${bookId}/details/`;
}

export function useBookListDetailPageUrl(listId: ID | string) {
  // Return URL for Book List detail page.
  return `/lists/${listId}/details/`;
}

export function useBookListAdminPageUrl(listId: ID | string) {
  // Return URL for Book List Django admin page.
  const config = useRuntimeConfig();
  return `${config.public.apiBase}/admin/books/list/${listId}/change/`;
}
