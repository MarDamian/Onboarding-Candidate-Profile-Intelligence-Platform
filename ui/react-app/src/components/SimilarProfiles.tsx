type Props = {
  candidateId: number;
};

export const SimilarProfiles = ({ candidateId }: Props) => {
  const url = `http://localhost:5174/?candidateId=${candidateId}`;

  return (
    <div className="w-full h-[calc(100vh-100px)]">
      <iframe
        src={url}
        scrolling="no"
        style={{
          width: "100%",
          height: "100%",
        }}
        title="Svelte Microfrontend"
      />
    </div>
  );
}
