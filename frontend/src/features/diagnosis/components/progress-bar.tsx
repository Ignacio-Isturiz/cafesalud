interface ProgressBarProps {
  current: number;
  total: number;
  value: number;
}

export function ProgressBar({ current, total, value }: ProgressBarProps) {
  return (
    <div className="question-progress" aria-label={`Pregunta ${current} de ${total}`}>
      <div><span>Pregunta {current} de {total}</span><strong>{Math.round(value)}%</strong></div>
      <div className="progress-track"><span style={{ width: `${value}%` }} /></div>
    </div>
  );
}
