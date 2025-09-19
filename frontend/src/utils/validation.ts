/**
 * Validation utilities for form fields
 */

export interface ValidationResult {
  isValid: boolean;
  error: string;
}

/**
 * Validates email format
 */
export const validateEmail = (email: string): ValidationResult => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  
  if (!email.trim()) {
    return { isValid: false, error: 'Email is required' };
  }
  
  if (!emailRegex.test(email)) {
    return { isValid: false, error: 'Please enter a valid email address' };
  }
  
  return { isValid: true, error: '' };
};

/**
 * Validates password strength
 */
export const validatePassword = (password: string): ValidationResult => {
  if (!password.trim()) {
    return { isValid: false, error: 'Password is required' };
  }
  
  if (password.length < 8) {
    return { isValid: false, error: 'Password must be at least 8 characters long' };
  }
  
  if (!/(?=.*[a-z])/.test(password)) {
    return { isValid: false, error: 'Password must contain at least one lowercase letter' };
  }
  
  if (!/(?=.*[A-Z])/.test(password)) {
    return { isValid: false, error: 'Password must contain at least one uppercase letter' };
  }
  
  if (!/(?=.*\d)/.test(password)) {
    return { isValid: false, error: 'Password must contain at least one number' };
  }
  
  return { isValid: true, error: '' };
};

/**
 * Validates username format
 */
export const validateUsername = (username: string): ValidationResult => {
  if (!username.trim()) {
    return { isValid: false, error: 'Username is required' };
  }
  
  if (username.length < 3) {
    return { isValid: false, error: 'Username must be at least 3 characters long' };
  }
  
  if (!/^[a-zA-Z0-9_]+$/.test(username)) {
    return { isValid: false, error: 'Username can only contain letters, numbers, and underscores' };
  }
  
  return { isValid: true, error: '' };
};

/**
 * Validates full name
 */
export const validateFullName = (fullName: string): ValidationResult => {
  if (!fullName.trim()) {
    return { isValid: false, error: 'Full name is required' };
  }
  
  return { isValid: true, error: '' };
};

/**
 * Validates password confirmation
 */
export const validatePasswordConfirmation = (password: string, confirmPassword: string): ValidationResult => {
  if (!confirmPassword.trim()) {
    return { isValid: false, error: 'Please confirm your password' };
  }
  
  if (confirmPassword !== password) {
    return { isValid: false, error: 'Passwords do not match' };
  }
  
  return { isValid: true, error: '' };
};

/**
 * Validates a field based on its type
 */
export const validateField = (fieldType: string, value: string, confirmValue?: string): ValidationResult => {
  switch (fieldType) {
    case 'email':
      return validateEmail(value);
    case 'password':
      return validatePassword(value);
    case 'username':
      return validateUsername(value);
    case 'full_name':
    case 'fullName':
      return validateFullName(value);
    case 'confirmPassword':
      if (!confirmValue) {
        return { isValid: false, error: 'Password confirmation is required' };
      }
      return validatePasswordConfirmation(confirmValue, value);
    default:
      return { isValid: true, error: '' };
  }
};

/**
 * Validates multiple fields at once
 */
export const validateFields = (fields: { [key: string]: string }): { [key: string]: string } => {
  const errors: { [key: string]: string } = {};
  
  Object.entries(fields).forEach(([fieldName, value]) => {
    let confirmValue: string | undefined;
    
    // Handle password confirmation
    if (fieldName === 'confirmPassword' && fields.password) {
      confirmValue = fields.password;
    }
    
    const result = validateField(fieldName, value, confirmValue);
    if (!result.isValid) {
      errors[fieldName] = result.error;
    }
  });
  
  return errors;
};
