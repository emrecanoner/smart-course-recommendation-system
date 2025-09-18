import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import courseReducer from './slices/courseSlice';
import recommendationReducer from './slices/recommendationSlice';
import enrollmentReducer from './slices/enrollmentSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    courses: courseReducer,
    recommendations: recommendationReducer,
    enrollments: enrollmentReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST'],
      },
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
