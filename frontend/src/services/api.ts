import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { 
  User, 
  LoginRequest, 
  RegisterRequest, 
  AuthResponse, 
  Course, 
  Recommendation,
  RecommendationRequest,
  ApiResponse,
  Category,
  Enrollment,
  EnrollmentCreate,
  EnrollmentUpdate,
  EnrollmentStats
} from '../types';

// API Configuration
const API_BASE_URL = 'http://localhost:8000/api/v1';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      timeout: 300000, // 5 minutes for AI recommendations
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add auth token
    this.api.interceptors.request.use(
      (config) => {
        const token = this.getToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor to handle errors
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Handle unauthorized access
          this.clearToken();
          // You might want to redirect to login here
        }
        return Promise.reject(error);
      }
    );
  }

  // Token management
  private getToken(): string | null {
    // In a real app, you'd get this from secure storage
    return localStorage.getItem('auth_token');
  }

  private setToken(token: string): void {
    localStorage.setItem('auth_token', token);
  }

  private clearToken(): void {
    localStorage.removeItem('auth_token');
  }

  // Authentication endpoints
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response: AxiosResponse<AuthResponse> = await this.api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    if (response.data.access_token) {
      this.setToken(response.data.access_token);
    }

    return response.data;
  }

  async register(userData: RegisterRequest): Promise<User> {
    const response: AxiosResponse<User> = await this.api.post('/auth/register', userData);
    return response.data;
  }

  async getCurrentUser(): Promise<User> {
    const response: AxiosResponse<User> = await this.api.get('/auth/test-token');
    return response.data;
  }

  // User endpoints
  async updateUser(userData: Partial<User>): Promise<User> {
    const response: AxiosResponse<User> = await this.api.put('/users/me', userData);
    return response.data;
  }

  // Course endpoints
  async getCourses(params?: {
    page?: number;
    size?: number;
    category?: string;
    search?: string;
  }): Promise<{ items: Course[]; total: number; page: number; size: number; pages: number; has_next: boolean; has_previous: boolean }> {
    const response = await this.api.get('/courses/', { params });
    return response.data;
  }

  async getCourse(courseId: number): Promise<Course> {
    const response: AxiosResponse<Course> = await this.api.get(`/courses/${courseId}`);
    return response.data;
  }

  async getCategories(): Promise<Category[]> {
    const response: AxiosResponse<Category[]> = await this.api.get('/courses/categories/');
    return response.data;
  }

  // Recommendation endpoints
  async getRecommendations(params?: {
    limit?: number;
    algorithm?: string;
  }): Promise<Recommendation[]> {
    const response: AxiosResponse<Recommendation[]> = await this.api.get('/recommendations/', { params });
    return response.data;
  }

  async generateRecommendations(request: RecommendationRequest): Promise<Recommendation[]> {
    const response: AxiosResponse<Recommendation[]> = await this.api.post('/recommendations/', request);
    return response.data;
  }

  async submitRecommendationFeedback(courseId: number, feedbackType: string): Promise<void> {
    await this.api.post('/recommendations/feedback', null, {
      params: { course_id: courseId, feedback_type: feedbackType },
    });
  }

  async getSimilarCourses(courseId: number, limit?: number): Promise<Recommendation[]> {
    const response: AxiosResponse<Recommendation[]> = await this.api.get(`/recommendations/similar/${courseId}`, {
      params: { limit },
    });
    return response.data;
  }

  async getDataRequirements(): Promise<{
    has_sufficient_data: boolean;
    interaction_count: number;
    enrollment_count: number;
    min_interactions_required: number;
    min_enrollments_required: number;
    interaction_progress: number;
    enrollment_progress: number;
    recommendations: {
      interactions_needed: number;
      enrollments_needed: number;
      suggestions: string[];
    };
  }> {
    const response: AxiosResponse = await this.api.get('/recommendations/data-requirements');
    return response.data;
  }

  async getDifficultyLevels(): Promise<string[]> {
    const response: AxiosResponse<string[]> = await this.api.get('/courses/difficulty-levels');
    return response.data;
  }

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    const response: AxiosResponse<{ status: string }> = await this.api.get('/health');
    return response.data;
  }

  // Logout
  logout(): void {
    this.clearToken();
  }

  // Enrollment methods
  async getEnrollments(): Promise<Enrollment[]> {
    const response: AxiosResponse<Enrollment[]> = await this.api.get('/enrollments/');
    return response.data;
  }

  async createEnrollment(enrollmentData: EnrollmentCreate): Promise<Enrollment> {
    const response: AxiosResponse<Enrollment> = await this.api.post('/enrollments/', enrollmentData);
    return response.data;
  }

  async checkEnrollment(courseId: number): Promise<{ is_enrolled: boolean }> {
    const response: AxiosResponse<{ is_enrolled: boolean }> = await this.api.get(`/enrollments/check/${courseId}`);
    return response.data;
  }

  async updateProgress(courseId: number, completionPercentage: number): Promise<any> {
    const response = await this.api.put(`/enrollments/progress/${courseId}`, null, {
      params: { completion_percentage: completionPercentage }
    });
    return response.data;
  }

  async getEnrollmentStats(): Promise<EnrollmentStats> {
    const response: AxiosResponse<EnrollmentStats> = await this.api.get('/enrollments/stats');
    return response.data;
  }

  async unenrollFromCourse(courseId: number): Promise<{ message: string }> {
    const response: AxiosResponse<{ message: string }> = await this.api.delete(`/enrollments/${courseId}`);
    return response.data;
  }

  // Analytics and Interaction Tracking methods
  async trackCourseView(courseId: number, sessionId?: string, deviceType?: string, referrer?: string): Promise<any> {
    const response = await this.api.post('/analytics/track/course-view', null, {
      params: { course_id: courseId, session_id: sessionId, device_type: deviceType, referrer }
    });
    return response.data;
  }

  async trackCourseLike(courseId: number, sessionId?: string, deviceType?: string, referrer?: string): Promise<any> {
    const response = await this.api.post('/analytics/track/course-like', null, {
      params: { course_id: courseId, session_id: sessionId, device_type: deviceType, referrer }
    });
    return response.data;
  }

  async trackCourseUnlike(courseId: number, sessionId?: string, deviceType?: string, referrer?: string): Promise<any> {
    const response = await this.api.post('/analytics/track/course-unlike', null, {
      params: { course_id: courseId, session_id: sessionId, device_type: deviceType, referrer }
    });
    return response.data;
  }

  async trackCourseEnroll(courseId: number, sessionId?: string, deviceType?: string, referrer?: string): Promise<any> {
    const response = await this.api.post('/analytics/track/course-enroll', null, {
      params: { course_id: courseId, session_id: sessionId, device_type: deviceType, referrer }
    });
    return response.data;
  }

  async trackCourseUnenroll(courseId: number, sessionId?: string, deviceType?: string, referrer?: string): Promise<any> {
    const response = await this.api.post('/analytics/track/course-unenroll', null, {
      params: { course_id: courseId, session_id: sessionId, device_type: deviceType, referrer }
    });
    return response.data;
  }

  async trackCourseComplete(courseId: number, completionPercentage: number, sessionId?: string, deviceType?: string, referrer?: string): Promise<any> {
    const response = await this.api.post('/analytics/track/course-complete', null, {
      params: { 
        course_id: courseId, 
        completion_percentage: completionPercentage,
        session_id: sessionId,
        device_type: deviceType,
        referrer
      }
    });
    return response.data;
  }

  async trackCourseRate(courseId: number, rating: number, sessionId?: string, deviceType?: string, referrer?: string): Promise<any> {
    const response = await this.api.post('/analytics/track/course-rate', null, {
      params: { course_id: courseId, rating, session_id: sessionId, device_type: deviceType, referrer }
    });
    return response.data;
  }

  async getUserInteractionSummary(): Promise<any> {
    const response = await this.api.get('/analytics/user/interaction-summary');
    return response.data;
  }

  async getUserPreferences(): Promise<any> {
    const response = await this.api.get('/analytics/user/preferences');
    return response.data;
  }

  async updateUserPreferences(preferences: any): Promise<any> {
    const response = await this.api.put('/analytics/user/preferences', preferences);
    return response.data;
  }

  async getUserLearningProfile(): Promise<any> {
    const response = await this.api.get('/analytics/user/learning-profile');
    return response.data;
  }

  async getUserInsights(): Promise<any> {
    const response = await this.api.get('/analytics/user/insights');
    return response.data;
  }
}

// Export singleton instance
export const apiService = new ApiService();
export default apiService;
