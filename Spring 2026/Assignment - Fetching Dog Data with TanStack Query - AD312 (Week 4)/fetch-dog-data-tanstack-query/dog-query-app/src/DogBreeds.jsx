import { useQuery } from '@tanstack/react-query';

function DogBreeds() {
    const { data, isPending, isError } = useQuery({
        queryKey: ['breeds'],
        queryFn: async () => {
            const res = await fetch('https://dogapi.dog/api/v2/breeds');
            return res.json();
        }
    });

    if (isPending) {
        return <p>Loading ...</p>
    }
    if (isError) {
        return <p>Error Loading</p>
    }

    return (
        <ul>
            {data.data.map((breed) => (
                <li key={breed.id}>{breed.attributes.name}</li>
            ))}
        </ul>
    );
}

export default DogBreeds;