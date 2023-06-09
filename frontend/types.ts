export type ID = number;

export interface User {
  id: ID;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  profile_image?: string;
  profile_image_thumbnail_small?: string;
  profile_image_thumbnail_large?: string;
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
  first_name?: string;
  middle_name?: string;
  last_name: string;
  description?: string;
  portrait?: string;
  portrait_thumbnail?: string;
}

export interface Book {
  id?: ID;
  user?: User;
  authors: Author[];
  title: string;
  publisher?: Publisher;
  year?: number;
  pages?: number;
  isbn?: string;
  description?: string;
  contents?: string;
  tags?: Tag[];
  cover_image?: string;
  cover_thumbnail_small?: string;
  cover_thumbnail_medium?: string;
  cover_thumbnail_large?: string;
  file?: string;
  created?: Date;
  updated?: Date;
}

export interface Note {
  id?: ID;
  user: ID;
  book: ID;
  text: string;
  created: Date;
  updated?: Date;
}

export interface ListPage<T> {
  count: number; // total count of items in the list
  page: number; // number of current page
  total_pages: number; // total number of pages in the list
  next: string; // API URL for next page or null
  previous: string; // API URL for previous page, or null
  results: T[]; // array of items on the current page
}

export interface AuthToken {
  auth_token: string;
}
export interface BookListItem {
  // This corresponds to `ListItemDetailSerializer`
  id: ID;
  order: number;
  book: Book;
  description: string;
  created: Date;
  updated: Date;
}

export interface BookList {
  // This corresponds to `ListListSerializer`
  id: ID;
  user: User;
  title: string;
  description: string;
  is_public: boolean;
  items: BookListItem[];
  created: Date;
  updated: Date;
}
