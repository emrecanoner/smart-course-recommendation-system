// User types
export interface User {
  id: number;
  email: string;
  username: string;
  full_name?: string;
  bio?: string;
  learning_goals?: string;
  preferred_categories?: string;
  skill_level?: string;
  time_commitment?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  last_login?: string;
}

// Authentication types
export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
  full_name?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

// Course types
export interface Category {
  id: number;
  name: string;
  description?: string;
  parent_id?: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Course {
  id: number;
  title: string;
  description?: string;
  short_description?: string;
  instructor?: string;
  duration_hours?: number;
  difficulty_level?: string;
  language: string;
  content_type?: string;
  has_certificate: boolean;
  is_free: boolean;
  price?: number;
  rating: number;
  rating_count: number;
  enrollment_count: number;
  completion_rate: number;
  is_active: boolean;
  is_featured: boolean;
  created_at: string;
  updated_at: string;
  published_at?: string;
  category?: Category;
}

// Recommendation types
export interface RecommendationRequest {
  limit?: number;
  algorithm?: string;
  categories?: string[];
  difficulty_level?: string;
  max_duration_hours?: number;
  content_type?: string;
}

export interface Recommendation {
  course_id: number;
  title: string;
  description?: string;
  short_description?: string;
  instructor?: string;
  duration_hours?: number;
  difficulty_level?: string;
  rating: number;
  rating_count: number;
  enrollment_count: number;
  is_free: boolean;
  price?: number;
  confidence_score: number;
  recommendation_reason?: string;
  category_name?: string;
}

// API Response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

// Navigation types
export type RootStackParamList = {
  Auth: undefined;
  Main: undefined;
  Login: undefined;
  Register: undefined;
  Home: undefined;
  Courses: undefined;
  CourseDetail: { courseId: number };
  Recommendations: undefined;
  Profile: undefined;
};

// State types
export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  isRegistering: boolean;
  error: string | null;
}

export interface CourseState {
  courses: Course[];
  categories: Category[];
  isLoading: boolean;
  error: string | null;
  selectedCourse: Course | null;
}

export interface RecommendationState {
  recommendations: Recommendation[];
  isLoading: boolean;
  error: string | null;
}
