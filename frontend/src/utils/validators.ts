export const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const validatePassword = (password: string): boolean => {
  // At least 8 characters, 1 uppercase, 1 lowercase, 1 number
  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
  return passwordRegex.test(password);
};

export const validateComponentName = (name: string): boolean => {
  return name.trim().length > 0 && name.trim().length <= 255;
};

export const validatePrice = (price: number): boolean => {
  return price > 0 && price <= 999999.99;
};
