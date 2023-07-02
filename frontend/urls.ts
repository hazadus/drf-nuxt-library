import { ID } from "@/types";

export function useBookDetailsPageUrl(bookId: ID | string) {
  // Return URL for Book detail page.
  return `/books/${bookId}/details/`;
}

export function useBookNotesPageUrl(bookId: ID | string) {
  // Return URL for Book notes page.
  return `/books/${bookId}/notes/`;
}

export function useBookListsPageUrl(bookId: ID | string) {
  // Return URL for Book lists page.
  return `/books/${bookId}/lists/`;
}

export function useBookListDetailPageUrl(listId: ID | string) {
  // Return URL for Book List detail page.
  return `/lists/${listId}/details/`;
}

export function useBookAdminPageUrl(bookId: ID | string) {
  // Return URL for Book Django admin page.
  const config = useRuntimeConfig();
  return `${config.public.apiBase}/admin/books/book/${bookId}/change/`;
}

export function useBookListAdminPageUrl(listId: ID | string) {
  // Return URL for Book List Django admin page.
  const config = useRuntimeConfig();
  return `${config.public.apiBase}/admin/books/list/${listId}/change/`;
}
