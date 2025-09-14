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
};

// Async thunks
export const fetchCourses = createAsyncThunk(
  'courses/fetchCourses',
  async (params?: {
    skip?: number;
    limit?: number;
    category?: string;
    search?: string;
  }, { rejectWithValue }) => {
    try {
      const courses = await apiService.getCourses(params);
      return courses;
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
        state.courses = action.payload;
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
      });
  },
});

export const { clearError, setSelectedCourse, clearCourses } = courseSlice.actions;
export default courseSlice.reducer;
