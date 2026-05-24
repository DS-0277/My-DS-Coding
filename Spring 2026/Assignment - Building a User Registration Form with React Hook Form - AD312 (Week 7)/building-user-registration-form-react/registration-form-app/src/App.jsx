import { useForm } from 'react-hook-form';
import { useEffect } from 'react';

export default function App() {
  const { register, formState: { errors, isSubmitting, isValid }, watch, handleSubmit, reset, setValue } = useForm({ mode: 'onChange' });

  const password = watch('password');

  const formData = watch();

  const onSubmit = async (data) => {
    console.log(data);
    await new Promise((resolve) => setTimeout(resolve, 2000));
    reset();
    localStorage.removeItem('formData');
  };

  useEffect(() => {
    localStorage.setItem('formData', JSON.stringify(formData));
  }, [formData]);

  useEffect(() => {
    setValue('fullName', 'John Michael');
  }, [])

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* Full Name */}
      <div>
        <label>Full Name</label>
        <input type="text" autoFocus {...register('fullName', {
          required: 'Full Name is required',
          minLength: {
            value: 3,
            message: 'Minimum characters of 3'
          }
        })}/>
        <p>{errors.fullName?.message}</p>
      </div>
      {/* Email Address */}
      <div>
        <label>Email</label>
        <input type="email" {...register('email', {
          required: 'Email is required',
          pattern: {
            value: /@.+\.com$/,
            message: 'Invalid email'
          }
        })} />
        <p>{errors.email?.message}</p>
      </div>
      {/* Password */}
      <div>
        <label>Password</label>
        <input type="password" {...register('password', {
          required: 'Password is required',
          minLength: {
            value: 8,
            message: 'Minimum characters of 8'
          },
          validate: (value) => 
            /[A-Z]/.test(value) &&
            /[a-z]/.test(value) &&
            /[0-9]/.test(value) ||
            'Must have uppercase, lowercase and number'
        })} />
        <p>{errors.password?.message}</p>
      </div>
      {/* Confirm Password */}
      <div>
        <label>Confirm Password</label>
        <input type="password" {...register('confirmPassword', {
          required: 'Confirm Password is required',
          validate: (value) => value === password || 'Passwords do not match'
        })} />
        <p>{errors.confirmPassword?.message}</p>
      </div>
      {/* Role */}
      <div>
        <label>Role</label>
        <select {...register('role', {
          required: 'Please select a role'
        })}>
          <option value="">Select a role...</option>
          <option value="Developer">Developer</option>
          <option value="Designer">Designer</option>
          <option value="Product Manager">Product Manager</option>
        </select>
        <p>{errors.role?.message}</p>
      </div>
      {/* Terms */}
      <div>
        <input type="checkbox" {...register('terms', {
          required: 'Please accept the terms'
        })} />
        <label>I accept the Terms & Conditions</label>
        <p>{errors.terms?.message}</p>
      </div>
      <button type="submit" disabled={!isValid || isSubmitting}>{isSubmitting ? 'Registering...' : 'Register'}</button>
    </form>
  );
}

// TEST CASES

// Normal Cases
// Case 1: ['John Michael', 'john@example.com', 'Pass1234', 'Pass1234', 'Developer', 'true'] ==> Got result as expected
// Case 2: ['Bob Henry', 'bob@example.com', 'Pass12345', 'Pass12345', 'Product Manager', 'true'] ==> Got result as expected
// Case 3: ['Mary Jane', 'mary@example.com', 'Pass123456', 'Pass123456', 'Designer', 'true'] ==> Got result as expected


// Edge Cases
// Case 1: In case the full name is 'Jo' ==> The message is "Minimum characters of 3"
// Case 2: In case the email has no '.com' ==> The message is "Invalid email"
// Case 3: In case the password is "Pass123" ==> The message is "Minimum characters of 8"