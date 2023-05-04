/*
* This module contains API abstraction functions.
*/
import { useFetch } from "nuxt/app";
import type { Book, ID } from '@/types';

function useApi () {
  const config = useRuntimeConfig();

  const get: typeof useFetch = (url, params) => {
    return useFetch(url, {
      params,
      baseURL: config.public.apiBase + "/api/v1",
      key: url.toString(),
    });
  };

  return { get };
}

export async function fetchAllBooks() {
  // Fetch list of all Books from API endpoint
  const { get } = useApi();
  return await get<Book[]>("/books/");
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