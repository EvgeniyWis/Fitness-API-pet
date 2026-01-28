"use client";

import { useState } from "react";
import { useRouter } from "next/router";
import { Button, Input, AuthFormContainer } from "@/shared/ui";
import { useRegisterMutation } from "@/shared/api";
import {
  validateEmail,
  validatePassword,
  validateName,
  validateConfirmPassword,
} from "@/shared/lib";

export const RegisterForm = () => {
  const router = useRouter();
  const [register, { isLoading }] = useRegisterMutation();
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    confirmPassword: "",
    name: "",
  });
  const [errors, setErrors] = useState<{
    email?: string;
    password?: string;
    confirmPassword?: string;
    name?: string;
  }>({});
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    // Очищаем ошибку при изменении поля
    if (errors[name as keyof typeof errors]) {
      setErrors((prev) => ({ ...prev, [name]: undefined }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});
    setSubmitError(null);
    setSuccessMessage(null);

    const newErrors: typeof errors = {};
    const nameError = validateName(formData.name);
    const emailError = validateEmail(formData.email);
    const passwordError = validatePassword(formData.password);
    const confirmPasswordError = validateConfirmPassword(
      formData.password,
      formData.confirmPassword
    );

    if (nameError) newErrors.name = nameError;
    if (emailError) newErrors.email = emailError;
    if (passwordError) newErrors.password = passwordError;
    if (confirmPasswordError) newErrors.confirmPassword = confirmPasswordError;

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

      const result = await register({
        username: formData.email,
        password: formData.password,
      }).unwrap();
      if (result.message?.includes("успешно")) {
        router.push("/login");
      } else {
        setSubmitError(result.message ?? "Ошибка регистрации");
      }
  };

  return (
    <AuthFormContainer
      title="Регистрация"
      footerText="Уже есть аккаунт?"
      footerLinkText="Войти"
      footerLinkHref="/login"
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          type="text"
          name="name"
          label="Имя"
          placeholder="Введите ваше имя"
          value={formData.name}
          onChange={handleChange}
          error={errors.name}
          disabled={isLoading}
          autoComplete="name"
        />

        <Input
          type="email"
          name="email"
          label="Email"
          placeholder="example@mail.com"
          value={formData.email}
          onChange={handleChange}
          error={errors.email}
          disabled={isLoading}
          autoComplete="email"
        />

        <Input
          type="password"
          name="password"
          label="Пароль"
          placeholder="Минимум 6 символов"
          value={formData.password}
          onChange={handleChange}
          error={errors.password}
          disabled={isLoading}
          autoComplete="new-password"
        />

        <Input
          type="password"
          name="confirmPassword"
          label="Подтвердите пароль"
          placeholder="Повторите пароль"
          value={formData.confirmPassword}
          onChange={handleChange}
          error={errors.confirmPassword}
          disabled={isLoading}
          autoComplete="new-password"
        />

        {successMessage && (
          <p className="text-sm text-green-600 font-medium" role="status">
            {successMessage}
          </p>
        )}
        {submitError && (
          <p className="text-sm text-red-600" role="alert">
            {submitError}
          </p>
        )}

        <Button
          type="submit"
          variant="primary"
          size="lg"
          className="w-full"
          disabled={isLoading}
        >
          {isLoading ? "Регистрация..." : "Зарегистрироваться"}
        </Button>
      </form>
    </AuthFormContainer>
  );
};
