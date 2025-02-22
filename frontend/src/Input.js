export function Input({ type, onChange }) {
    return (
      <input
        type={type}
        onChange={onChange}
        className="border rounded px-3 py-2 w-full"
      />
    );
  }
  