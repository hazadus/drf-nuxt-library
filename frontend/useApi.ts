/*
* This module contains API abstraction functions.
*/
import { useFetch } from "nuxt/app";
import type { Book, ID, ListPage } from '@/types';

function useApi (query: Object | undefined = undefined) {
  const config = useRuntimeConfig();

  // Reference: https://nuxt.com/docs/api/composables/use-fetch
  const get: typeof useFetch = (url, params) => {
    return useFetch(url, {
      params: query,
      baseURL: config.public.apiBase + "/api/v1",
      key: url.toString(),
    });
  };

  return { get };
}

export async function fetchAllBooks(page: number = 1, query: string | undefined = undefined) {
  // Fetch paginated list of all Books from API endpoint.
  // This will return the first page of the list by default.
  // Use `query` to filter list by a srting.
  const { get } = useApi({ page: page, query: query, });
  return await get<ListPage<Book>>("/books/");
}

export async function fetchBook(bookId: ID | string) {
  // Fetch individual Book data by it's ID from API endpoint
  const { get } = useApi();
  return await get<Book>(`/books/${bookId}/`);
}

export function getMediaUrl(relativeLink: string) {
  // Build full URL to media file from relative link returned by API in FileField's (e.g. Book.cover_image or User.profile_image).
  const config = useRuntimeConfig();
  return `${config.public.apiBase}${relativeLink}`;
}