import { useQuery } from '@tanstack/react-query';

function DogGroups() {
    const { data, isPending, isError } = useQuery({
        queryKey: ['groups'],
        queryFn: async () => {
            const res = await fetch('https://dogapi.dog/api/v2/groups');
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
            {data.data.map((group) => (
                <li key={group.id}>{group.attributes.name}</li>
            ))}
        </ul>
    );
}

export default DogGroups;