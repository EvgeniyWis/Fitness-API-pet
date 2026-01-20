export const validateEmail = (email: string): string | undefined => {
  if (!email) {
    return "Email обязателен";
  }
  if (!/\S+@\S+\.\S+/.test(email)) {
    return "Некорректный email";
  }
  return undefined;
};

export const validatePassword = (
  password: string,
  minLength = 6
): string | undefined => {
  if (!password) {
    return "Пароль обязателен";
  }
  if (password.length < minLength) {
    return `Пароль должен содержать минимум ${minLength} символов`;
  }
  return undefined;
};

export const validateName = (
  name: string,
  minLength = 2
): string | undefined => {
  if (!name.trim()) {
    return "Имя обязательно";
  }
  if (name.trim().length < minLength) {
    return `Имя должно содержать минимум ${minLength} символа`;
  }
  return undefined;
};

export const validateConfirmPassword = (
  password: string,
  confirmPassword: string
): string | undefined => {
  if (!confirmPassword) {
    return "Подтвердите пароль";
  }
  if (password !== confirmPassword) {
    return "Пароли не совпадают";
  }
  return undefined;
};
