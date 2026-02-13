interface Props {
  candidateId: number;
}

const BASE_URL = import.meta.env.VITE_SVELTE_URL

export const SimilarProfiles = ({ candidateId }: Props) => {
  const url = `${BASE_URL}/?id=${candidateId}`;

  return (
    <div className="w-full h-[calc(100vh-100px)] overflow-hidden">
      <iframe
        src={url}
        scrolling="no"
        width="100%"
        height="100%"
        style={{
          border: "none",
        }}
        title="Svelte Microfrontend"
        loading="lazy"
      />
    </div>
  );
}