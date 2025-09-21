import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { Recommendation, RecommendationRequest, RecommendationState } from '../../types';
import apiService from '../../services/api';

// Initial state
const initialState: RecommendationState = {
  recommendations: [],
  isLoading: false,
  error: null,
};

// Async thunks
export const fetchRecommendations = createAsyncThunk(
  'recommendations/fetchRecommendations',
  async (params: {
    limit?: number;
    algorithm?: string;
  } = {}, { rejectWithValue }) => {
    try {
      const recommendations = await apiService.getRecommendations(params);
      return recommendations;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch recommendations');
    }
  }
);

export const generateRecommendations = createAsyncThunk(
  'recommendations/generateRecommendations',
  async (request: RecommendationRequest, { rejectWithValue }) => {
    try {
      const recommendations = await apiService.generateRecommendations(request);
      return recommendations;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to generate recommendations');
    }
  }
);

export const submitFeedback = createAsyncThunk(
  'recommendations/submitFeedback',
  async ({ courseId, feedbackType }: { courseId: number; feedbackType: string }, { rejectWithValue }) => {
    try {
      await apiService.submitRecommendationFeedback(courseId, feedbackType);
      return { courseId, feedbackType };
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to submit feedback');
    }
  }
);

export const fetchSimilarCourses = createAsyncThunk(
  'recommendations/fetchSimilarCourses',
  async ({ courseId, limit }: { courseId: number; limit?: number }, { rejectWithValue }) => {
    try {
      const recommendations = await apiService.getSimilarCourses(courseId, limit);
      return recommendations;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch similar courses');
    }
  }
);

// Recommendation slice
const recommendationSlice = createSlice({
  name: 'recommendations',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    clearRecommendations: (state) => {
      state.recommendations = [];
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch recommendations
      .addCase(fetchRecommendations.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchRecommendations.fulfilled, (state, action) => {
        state.isLoading = false;
        state.recommendations = action.payload;
        state.error = null;
      })
      .addCase(fetchRecommendations.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Generate recommendations
      .addCase(generateRecommendations.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(generateRecommendations.fulfilled, (state, action) => {
        state.isLoading = false;
        state.recommendations = action.payload;
        state.error = null;
      })
      .addCase(generateRecommendations.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Submit feedback
      .addCase(submitFeedback.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(submitFeedback.fulfilled, (state) => {
        state.isLoading = false;
        state.error = null;
      })
      .addCase(submitFeedback.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Fetch similar courses
      .addCase(fetchSimilarCourses.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchSimilarCourses.fulfilled, (state, action) => {
        state.isLoading = false;
        state.recommendations = action.payload;
        state.error = null;
      })
      .addCase(fetchSimilarCourses.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const { clearError, clearRecommendations } = recommendationSlice.actions;
export default recommendationSlice.reducer;
