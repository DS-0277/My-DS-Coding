import { useQuery } from '@tanstack/react-query';

function DogFacts() {
    const { data, isPending, isError } = useQuery({
        queryKey: ['facts'],
        queryFn: async () => {
            const res = await fetch('https://dogapi.dog/api/v2/facts');
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
            {data.data.map((fact) => (
                <li key={fact.id}>{fact.attributes.body}</li>
            ))}
        </ul>
    );
}

export default DogFacts;