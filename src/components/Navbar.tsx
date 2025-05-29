import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { navbarStyles } from '../styles/components';

const Navbar = () => {
  const router = useRouter();

  return (
    <AppBar position="fixed" sx={navbarStyles.appBar}>
      <Toolbar>
        <Link href="/" passHref>
          <Box component="a" sx={navbarStyles.logo}>
            <img src="/images/athly.png" alt="Athly" style={{ height: '100%', borderRadius: '50%' }} />
          </Box>
        </Link>
        
        <Box sx={{ flexGrow: 1 }} />
        
        <Link href="/" passHref>
          <Typography 
            component="a"
            sx={{
              ...navbarStyles.link,
              ...(router.pathname === '/' && navbarStyles.activeLink)
            }}
          >
            Home
          </Typography>
        </Link>
        
        <Link href="/about" passHref>
          <Typography 
            component="a"
            sx={{
              ...navbarStyles.link,
              ...(router.pathname === '/about' && navbarStyles.activeLink)
            }}
          >
            About
          </Typography>
        </Link>
        
        <Link href="/pricing" passHref>
          <Typography 
            component="a"
            sx={{
              ...navbarStyles.link,
              ...(router.pathname === '/pricing' && navbarStyles.activeLink)
            }}
          >
            Pricing
          </Typography>
        </Link>
        
        <Link href="/contact" passHref>
          <Typography 
            component="a"
            sx={{
              ...navbarStyles.link,
              ...(router.pathname === '/contact' && navbarStyles.activeLink)
            }}
          >
            Contact
          </Typography>
        </Link>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar; 