/*
* This module contains API abstraction functions.
*/
import { useFetch } from "nuxt/app";
import type { Book, ID, ListPage, Publisher, Author } from '@/types';

export function getMediaUrl(relativeLink: string) {
  // Build full URL to media file from relative link returned by API in FileField's (e.g. Book.cover_image or User.profile_image).
  const config = useRuntimeConfig();
  return `${config.public.apiBase}${relativeLink}`;
}

function useApi (
  query: Object | undefined = undefined,
  method: string = "GET",
  formData: FormData | Object | undefined = undefined
  ) {
  const config = useRuntimeConfig();

  // Reference: https://nuxt.com/docs/api/composables/use-fetch
  const get: typeof useFetch = (url, params) => {
    return useFetch(url, {
      params: query,
      baseURL: config.public.apiBase + "/api/v1",
      key: url.toString(),
      method: method as any,
      body: formData,
    });
  };

  return { get };
}

export async function fetchAllBooks(page: number = 1, query: string | undefined = undefined) {
  // Fetch paginated list of all Books from API endpoint.
  // This will return the first page of the list by default.
  // Use `query` to filter list by a string.
  const { get } = useApi({ page: page, query: query, });
  return await get<ListPage<Book>>("/books/");
}

export async function fetchBook(bookId: ID | string) {
  // Fetch individual Book data by it's ID from API endpoint
  const { get } = useApi();
  return await get<Book>(`/books/${bookId}/`);
}

export async function createNewBook(book: Book) {
  // Create new Book.
  let authorIds: number[] = [];

  // Convert array of `Authors` to array of ids for backend.
  book.authors.forEach((a) => authorIds.push(a.id));

  const formData = {
    title: book.title,
    authors: authorIds,
    publisher: book.publisher?.id,  // pass only ID, not object!
    year: book.year,
    pages: book.pages,
    description: book.description,
    contents: book.contents,
  }

  const { get } = useApi(undefined, "POST", formData);
  return await get<Book>("/books/create/");
}

export async function fetchAllPublishers(query: string | undefined = undefined) {
  // Fetch full list of all publishers, without pagination from API endpoint
  // Use `query` to filter list by a string.
  const { get } = useApi({ query: query, });
  return await get<Publisher[]>("/publishers/");
}

export async function createNewPublisher(title: string) {
  // Create new Publisher named `title`.
  let formData = new FormData();
  formData.append("title", title);
  const { get } = useApi(undefined, "POST", formData);
  return await get<Publisher>("/publishers/");
}

export async function fetchAllAuthors(query: string | undefined = undefined) {
  // Fetch full list of all authors, without pagination from API endpoint
  // Use `query` to filter list by a string by author's last name.
  const { get } = useApi({ query: query, });
  return await get<Author[]>("/authors/");
}

export async function createNewAuthor(formData: FormData) {
  // Create new Author.
  const { get } = useApi(undefined, "POST", formData);
  return await get<Author>("/authors/create/");
}
