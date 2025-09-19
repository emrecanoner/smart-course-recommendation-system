import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { RootState, AppDispatch } from '../index';
import apiService from '../../services/api';
import { 
  Enrollment, 
  EnrollmentCreate, 
  EnrollmentUpdate, 
  EnrollmentStats 
} from '../../types';

// Initial state
const initialState = {
  enrollments: [] as Enrollment[],
  isLoading: false,
  error: null as string | null,
  stats: null as EnrollmentStats | null,
  enrollmentStatus: {} as Record<number, boolean>,
};

// Async thunks
export const fetchEnrollments = createAsyncThunk(
  'enrollments/fetchEnrollments',
  async (_, { rejectWithValue }) => {
    try {
      const enrollments = await apiService.getEnrollments();
      return enrollments;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch enrollments');
    }
  }
);

export const createEnrollment = createAsyncThunk(
  'enrollments/createEnrollment',
  async (enrollmentData: EnrollmentCreate, { rejectWithValue }) => {
    try {
      const enrollment = await apiService.createEnrollment(enrollmentData);
      return enrollment;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to create enrollment');
    }
  }
);

export const checkEnrollment = createAsyncThunk(
  'enrollments/checkEnrollment',
  async (courseId: number, { rejectWithValue }) => {
    try {
      const result = await apiService.checkEnrollment(courseId);
      return { courseId, isEnrolled: result.is_enrolled };
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to check enrollment');
    }
  }
);

export const unenrollFromCourse = createAsyncThunk(
  'enrollments/unenrollFromCourse',
  async (courseId: number, { rejectWithValue }) => {
    try {
      const result = await apiService.unenrollFromCourse(courseId);
      return { courseId, message: result.message };
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to unenroll from course');
    }
  }
);

export const updateProgress = createAsyncThunk(
  'enrollments/updateProgress',
  async ({ courseId, completionPercentage }: { courseId: number; completionPercentage: number }, { rejectWithValue }) => {
    try {
      const result = await apiService.updateProgress(courseId, completionPercentage);
      return { courseId, enrollment: result.enrollment };
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to update progress');
    }
  }
);

export const fetchEnrollmentStats = createAsyncThunk(
  'enrollments/fetchEnrollmentStats',
  async (_, { rejectWithValue }) => {
    try {
      const stats = await apiService.getEnrollmentStats();
      return stats;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch enrollment stats');
    }
  }
);

// Slice
const enrollmentSlice = createSlice({
  name: 'enrollments',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    clearEnrollments: (state) => {
      state.enrollments = [];
      state.stats = null;
    },
  },
  extraReducers: (builder) => {
    // Fetch enrollments
    builder
      .addCase(fetchEnrollments.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchEnrollments.fulfilled, (state, action) => {
        state.isLoading = false;
        state.enrollments = action.payload;
        // Update enrollment status for all enrolled courses
        action.payload.forEach((enrollment: any) => {
          state.enrollmentStatus[enrollment.course_id] = true;
        });
        state.error = null;
      })
      .addCase(fetchEnrollments.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });

    // Create enrollment
    builder
      .addCase(createEnrollment.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(createEnrollment.fulfilled, (state, action) => {
        state.isLoading = false;
        state.enrollments.unshift(action.payload);
        // Update enrollment status for this course
        state.enrollmentStatus[action.payload.course_id] = true;
        state.error = null;
      })
      .addCase(createEnrollment.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });

    // Check enrollment
    builder
      .addCase(checkEnrollment.fulfilled, (state, action) => {
        const { courseId, isEnrolled } = action.payload;
        state.enrollmentStatus[courseId] = isEnrolled;
      })
      .addCase(checkEnrollment.rejected, (state, action) => {
        state.error = action.payload as string;
      })
      .addCase(unenrollFromCourse.fulfilled, (state, action) => {
        const { courseId } = action.payload;
        state.enrollmentStatus[courseId] = false;
        // Remove from enrollments array
        state.enrollments = state.enrollments.filter(e => e.course_id !== courseId);
      })
      .addCase(unenrollFromCourse.rejected, (state, action) => {
        state.error = action.payload as string;
      });

    // Update progress
    builder
      .addCase(updateProgress.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(updateProgress.fulfilled, (state, action) => {
        state.isLoading = false;
        const { courseId, enrollment } = action.payload;
        const index = state.enrollments.findIndex(e => e.course_id === courseId);
        if (index !== -1) {
          state.enrollments[index] = enrollment;
        }
        state.error = null;
      })
      .addCase(updateProgress.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });

    // Fetch enrollment stats
    builder
      .addCase(fetchEnrollmentStats.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchEnrollmentStats.fulfilled, (state, action) => {
        state.isLoading = false;
        state.stats = action.payload;
        state.error = null;
      })
      .addCase(fetchEnrollmentStats.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const { clearError, clearEnrollments } = enrollmentSlice.actions;

// Selectors
export const selectEnrollments = (state: RootState) => state.enrollments.enrollments;
export const selectEnrollmentLoading = (state: RootState) => state.enrollments.isLoading;
export const selectEnrollmentError = (state: RootState) => state.enrollments.error;
export const selectEnrollmentStats = (state: RootState) => state.enrollments.stats;

export default enrollmentSlice.reducer;
