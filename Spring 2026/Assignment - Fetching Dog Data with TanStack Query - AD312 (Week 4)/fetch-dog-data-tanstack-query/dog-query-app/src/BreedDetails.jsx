import { useQuery } from '@tanstack/react-query';

function BreedDetails({ id }) {
    const { data, isPending, isError } = useQuery({
        queryKey: ['breed', id],
        queryFn: async () => {
            const res = await fetch(`https://dogapi.dog/api/v2/breeds/${id}`);
            return res.json();
        }
    });

    if (!id) {
        return <p>No ID is provided</p>
    }

    if (isPending) {
        return <p>Loading ...</p>
    }
    if (isError) {
        return <p>Error Loading</p>
    }

    return (
        <div>
            <p>{data.data.attributes.name}</p>
            <p>{data.data.attributes.description}</p>
        </div>
    );
}

export default BreedDetails;