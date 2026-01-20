"use client";

import React from "react";

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, className = "", ...props }, ref) => {
    const baseStyles =
      "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 transition-colors";
    const normalStyles =
      "border-gray-300 focus:border-blue-500 focus:ring-blue-500";
    const errorStyles =
      "border-red-500 focus:border-red-500 focus:ring-red-500";

    const inputClassName = `${baseStyles} ${
      error ? errorStyles : normalStyles
    } ${className}`.trim();

    return (
      <div className="w-full">
        {label && (
          <label className="block text-sm font-medium text-gray-700 mb-1">
            {label}
          </label>
        )}
        <input ref={ref} className={inputClassName} {...props} />
        {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
      </div>
    );
  }
);

Input.displayName = "Input";
