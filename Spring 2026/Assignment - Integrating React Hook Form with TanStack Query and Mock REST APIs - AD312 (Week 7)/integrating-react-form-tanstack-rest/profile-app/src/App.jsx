import { useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';

export default function App() {
  const { register, handleSubmit, reset, setError, formState: { errors, isDirty } } = useForm();

  const queryClient = useQueryClient();

  const { data } = useQuery({
    queryKey: ['userProfile'],
    queryFn: async () => {
      const response = await fetch('http://localhost:3001/profile');
      return response.json();
    }
  });

  useEffect(() => {
    if (data) {
      reset(data);
    }
  }, [data, reset]);

  const mutation = useMutation({
    mutationFn: async (formData) => {
      const response = await fetch('http://localhost:3001/profile', 
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(formData)
        }
      );
      return response.json();
    },

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ['userProfile']
      });
    },

    onError: () => {
      setError('email', {
        message: 'Update failed'
      });
    }
  });

  const onSubmit = (formData) => {
    mutation.mutate(formData);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input placeholder="Username" {...register('username')} />
      <input placeholder="Email" {...register('email')} />
      {errors.email && (<p>{errors.email.message}</p>)}
      <input placeholder="Bio" {...register('bio')} />
      <button type="submit" disabled={!isDirty || mutation.isPending}>Save</button>
    </form>
  );
}