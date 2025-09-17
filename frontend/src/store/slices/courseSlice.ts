import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { Course, Category, CourseState } from '../../types';
import apiService from '../../services/api';

// Initial state
const initialState: CourseState = {
  courses: [],
  categories: [],
  isLoading: false,
  error: null,
  selectedCourse: null,
  pagination: {
    currentPage: 1,
    totalPages: 1,
    totalItems: 0,
    itemsPerPage: 20,
    hasNextPage: false,
    hasPreviousPage: false,
  },
};

// Async thunks
export const fetchCourses = createAsyncThunk(
  'courses/fetchCourses',
  async (params: {
    page?: number;
    limit?: number;
    category?: string;
    search?: string;
  } = {}, { rejectWithValue }) => {
    try {
      const page = params?.page || 1;
      const limit = params?.limit || 20;
      const skip = (page - 1) * limit;
      
      const response = await apiService.getCourses({
        page,
        size: limit,
        category: params?.category,
        search: params?.search,
      });
      
      return {
        courses: response.items,
        pagination: {
          currentPage: response.page,
          totalPages: response.pages,
          totalItems: response.total,
          itemsPerPage: response.size,
          hasNextPage: response.has_next,
          hasPreviousPage: response.has_previous,
        }
      };
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch courses');
    }
  }
);

export const fetchCourse = createAsyncThunk(
  'courses/fetchCourse',
  async (courseId: number, { rejectWithValue }) => {
    try {
      const course = await apiService.getCourse(courseId);
      return course;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch course');
    }
  }
);

export const fetchCategories = createAsyncThunk(
  'courses/fetchCategories',
  async (_, { rejectWithValue }) => {
    try {
      const categories = await apiService.getCategories();
      return categories;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch categories');
    }
  }
);

// Course slice
const courseSlice = createSlice({
  name: 'courses',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setSelectedCourse: (state, action: PayloadAction<Course | null>) => {
      state.selectedCourse = action.payload;
    },
    clearCourses: (state) => {
      state.courses = [];
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch courses
      .addCase(fetchCourses.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchCourses.fulfilled, (state, action) => {
        state.isLoading = false;
        state.courses = action.payload.courses;
        state.pagination = action.payload.pagination;
        state.error = null;
      })
      .addCase(fetchCourses.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Fetch single course
      .addCase(fetchCourse.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchCourse.fulfilled, (state, action) => {
        state.isLoading = false;
        state.selectedCourse = action.payload;
        state.error = null;
      })
      .addCase(fetchCourse.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Fetch categories
      .addCase(fetchCategories.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchCategories.fulfilled, (state, action) => {
        state.isLoading = false;
        state.categories = action.payload;
        state.error = null;
      })
      .addCase(fetchCategories.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const { clearError, setSelectedCourse, clearCourses } = courseSlice.actions;
export default courseSlice.reducer;
