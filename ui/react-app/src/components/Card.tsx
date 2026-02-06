import React, { ReactNode } from 'react';

interface CardProps {
  title?: ReactNode;
  subtitle?: ReactNode;
  children: ReactNode;
  className?: string;           // ← nuevo: clases extras
  bodyClassName?: string;       // ← nuevo: para personalizar card-body
}

export const Card = ({
  title,
  subtitle,
  children,
  className = '',
  bodyClassName = '',
}: CardProps) => {
  return (
    <div className={`card bg-base-100 shadow-xl rounded-xl ${className}`}>
      {(title || subtitle) && (
        <div className="card-title px-6 pt-6 pb-2">
          {title && <h2 className="text-2xl font-bold">{title}</h2>}
          {subtitle && <p className="text-base-content/70 mt-1">{subtitle}</p>}
        </div>
      )}

      <div className={`card-body px-6 pb-6 pt-2 ${bodyClassName}`}>
        {children}
      </div>
    </div>
  );
};