import type { ReactNode } from 'react';

interface CardProps {
  title?: string | ReactNode;
  subtitle?: string | ReactNode;
  children?: ReactNode;
}

export const Card = ({
  title,
  subtitle,
  children,
}:CardProps) => {
  return (
    <section className="card">
      {(title || subtitle) && (
        <div className="card-header">
          {title && (
            <h2 className="card-title">
              {title}
            </h2>
          )}
          {subtitle && (
            <div className="card-subtitle">
              {subtitle}
            </div>
          )}
        </div>
      )}

      <div className="card-body">
        {children}
      </div>
    </section>
  );
};