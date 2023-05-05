export type ID = number;

export interface User {
  id: ID;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  profile_image: string;
  is_active: boolean;
  is_staff: boolean;
  is_superuser: boolean;
  last_login: Date;
  date_joined: Date;
}

export interface Tag {
  id: ID;
  title: string;
  user: ID;
}

export interface Publisher {
  id: ID;
  title: string;
}

export interface Author {
  id: ID;
  first_name: string;
  middle_name?: string;
  last_name: string;
  description?: string;
  portrait?: string;
}

export interface Book {
  id: ID;
  user: User;
  authors: Author[];
  title: string;
  year: number;
  publisher: Publisher;
  isbn: string;
  description: string;
  contents: string;
  tags: Tag[];
  cover_image: string;
  file: string;
  created: Date;
  updated: Date;
}

export interface ListPage<T> {
  count: number;  // total count of items in the list 
  page: number;   // number of current page
  total_pages: number;  // total number of pages in the list
  next: string;   // API URL for next page or null
  previous: string;     // API URL for previous page, or null
  results: T[];  // array of items on the current page
}