type Props = {
  candidateId: number;
  height?: number;
};

export default function SvelteMicrofrontend({ candidateId, height = 520 }: Props) {
  const url = `http://localhost:5174/?candidateId=${candidateId}`;

  return (
    <div style={{ width: "100%", height }}>
      <iframe
        src={url}
        style={{
          width: "100%",
          height: "100%",
          border: "none",
          borderRadius: "12px",
        }}
        title="Svelte Microfrontend"
      />
    </div>
  );
}
