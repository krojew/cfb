//! This file is auto-generated by cfbc.
use super::scalars_with_same_size_generated as reader;

pub mod example {
    #![allow(unused_imports)]

    use super::reader::example as reader;
    use flatbuffers::{self, Follow};
    use flatbuffers_verifier::{
        try_follow_uoffset, Error, Result, StringVerifier, VectorVerifier, Verify,
        MAX_OFFSET_LOC,
    };

    impl<'a> Verify for reader::Point<'a> {
        fn verify(&self) -> Result {
            let tab = self._tab;
            let buf = tab.buf;
            let buf_len = buf.len();

            if tab.loc > MAX_OFFSET_LOC || tab.loc + flatbuffers::SIZE_SOFFSET > buf_len {
                return Err(Error::OutOfBounds);
            }

            let vtab_loc = {
                let soffset_slice = &buf[tab.loc..];
                let soffset = flatbuffers::read_scalar::<flatbuffers::SOffsetT>(soffset_slice);
                if soffset >= 0 {
                    tab.loc.checked_sub(soffset as usize)
                } else {
                    soffset
                        .checked_neg()
                        .and_then(|foffset| tab.loc.checked_add(foffset as usize))
                }
            }
            .ok_or(Error::OutOfBounds)?;
            if vtab_loc
                .checked_add(flatbuffers::SIZE_VOFFSET + flatbuffers::SIZE_VOFFSET)
                .filter(|loc| *loc <= buf_len)
                .is_none()
            {
                return Err(Error::OutOfBounds);
            }

            let vtab = tab.vtable();
            let vtab_num_bytes = vtab.num_bytes();
            if vtab_loc
                .checked_add(vtab_num_bytes)
                .filter(|loc| *loc <= buf_len)
                .is_none()
            {
                return Err(Error::OutOfBounds);
            }
            let object_inline_num_bytes = vtab.object_inline_num_bytes();
            if tab
                .loc
                .checked_add(object_inline_num_bytes)
                .filter(|loc| *loc <= buf_len)
                .is_none()
            {
                return Err(Error::OutOfBounds);
            }

            for i in 0..vtab.num_fields() {
                let voffset = vtab.get_field(i) as usize;
                if (voffset > 0 && voffset < flatbuffers::SIZE_SOFFSET)
                    || voffset >= object_inline_num_bytes
                {
                    return Err(Error::OutOfBounds);
                }
            }

            if Self::VT_X as usize + flatbuffers::SIZE_VOFFSET
                <= vtab_num_bytes
            {
                let voffset = vtab.get(Self::VT_X) as usize;
                if voffset > 0 && object_inline_num_bytes - voffset < 8 {
                    return Err(Error::OutOfBounds);
                }
            }

            if Self::VT_Y as usize + flatbuffers::SIZE_VOFFSET
                <= vtab_num_bytes
            {
                let voffset = vtab.get(Self::VT_Y) as usize;
                if voffset > 0 && object_inline_num_bytes - voffset < 8 {
                    return Err(Error::OutOfBounds);
                }
            }

            Ok(())
        }
    }
}
